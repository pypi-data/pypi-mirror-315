"""Helper functions for writing publication network functions."""

import os
import re
from typing import Sequence, cast

__all__ = [
    "node_file_parts",
    "node_gen_file_name",
    "node_list_files",
    "node_gen_id_label",
    "node_id_label_parts",
    "edge_gen_file_name",
    "edge_key",
    "edge_parts",
    "edge_list_files",
    "edge_file_parts",
    "edge_gen_header",
    "edge_header_parts",
    "is_node_file",
    "is_edge_file",
    "select_graph_components",
]

NODE_PATH_REGEX = re.compile(r"(?P<node>\w+)_nodes.(?P<ext>[\w\.]+)")
EDGE_PATH_REGEX = re.compile(r"(?P<n1>\w+)_(?P<n2>\w+)_edges.(?P<ext>[\w\.]+)")
EDGE_KEY_DELIM = "-"


def is_node_file(file_name: str) -> bool:
    return re.search(NODE_PATH_REGEX, file_name) is not None


def is_edge_file(file_name: str) -> bool:
    return re.search(EDGE_PATH_REGEX, file_name) is not None


def edge_key(node_1: str, node_2: str) -> str:
    """Generate a dictionary key for the given pair of nodes.

    Known future issue:
        If we need directed edges, the order of nodes in the file name
        may be important. Add in a directed keyword argument, if true
        look for files only with the nodes in the order they were
        provided otherwise look for both. Another option is to not
        only check the file name but check the header for the START_ID
        and END_ID node types.

    See Also
    --------
    `edge_parts` for going in the other direction.

    """
    return EDGE_KEY_DELIM.join(sorted((node_1, node_2)))


def edge_parts(key: str | tuple[str, str]) -> tuple[str, str]:
    """Break an edge key into its nodes.

    See Also
    --------
    `edge_key` for going in the other direction.

    """
    # Often gets called in places where an edge could be described as a tuple
    # of nodes or a key, so if already in tuple form, harmlessly pass back.
    if isinstance(key, tuple):
        return key

    parts = key.split(EDGE_KEY_DELIM)
    if len(parts) != 2:
        raise ValueError(
            f"{parts} has wrong number of parts. Key should have exactly one"
            f' "{EDGE_KEY_DELIM}".'
        )

    return cast(tuple[str, str], tuple(sorted(parts)))


def edge_file_parts(file_name: str) -> tuple[str, str]:
    r"""Return the edge name and its file extension.

    Assumes the convention f"{node}_{node_or_type}_edges.{ext}".

    Parameters
    ----------
    file_name : str
        The name of the file.

    """
    name_matches = re.search(EDGE_PATH_REGEX, file_name)

    if name_matches is None:
        raise NameError("File name does not match naming conventions.")

    name_parts = name_matches.groupdict()

    return (edge_key(name_parts["n1"], name_parts["n2"]), name_parts["ext"])


def node_file_parts(file_name: str):
    r"""Return the edge name and its file extension.

    Assumes the convention f"{node}_nodes.{ext}".

    Parameters
    ----------
    file_name : str
        The name of the file.

    """
    name_parts = re.search(NODE_PATH_REGEX, file_name)

    if name_parts is None:
        raise NameError("File name does not match naming conventions.")

    return name_parts.groups()


def node_gen_file_name(node: str, ext: str, data_dir: str) -> str:
    """Create the path to a file the given node can be saved to."""
    return os.path.join(data_dir, f"{node}_nodes.{ext}")


def edge_gen_file_name(edge: str, ext: str, data_dir: str) -> tuple[str, str]:
    """Create the path to a file the given edge can be saved to."""
    n1, n2 = edge_parts(edge)
    data_path = os.path.join(data_dir, f"{n1}_{n2}_edges.{ext}")
    header_path = os.path.join(data_dir, f"{n1}_{n2}_edge_header.tsv")
    return (data_path, header_path)


def node_list_files(
    graph_dir: str, nodes: list[str] | None = None
) -> list[str]:
    """Return preferred node files in the graph_dir.

    Generally lists all node files in a graph. If multiple files contain the
    same node type, only one file is added to the list. Preference is given by
    file type. Binary (feather) is given top priority since it is the fastest
    to read.

    If nodes is provided, only return files for the nodes in the list.
    Otherwise, return all node files.
    """

    def node_find_file(
        node: str, path_dict: dict[str, dict[str, str]]
    ) -> str | None:
        """Return the file path for a node."""
        try:
            available_files = path_dict[node]
        except KeyError:
            return None

        ext_preference = ["feather", "tsv", "tsv.gz"]
        for ext in ext_preference:
            try:
                return available_files[ext]
            except KeyError:
                continue

        raise FileNotFoundError(
            f'No file found for node "{node}" with a supported file extension.'
        )

    files = os.listdir(graph_dir)
    node_files = [
        (m.groupdict(), os.path.join(graph_dir, m.group()))
        for m in (re.search(NODE_PATH_REGEX, f) for f in files)
        if m is not None
    ]
    nodes = nodes or list({n[0]["node"] for n in node_files})
    path_dict: dict[str, dict[str, str]] = {}
    for n in nodes:
        path_dict[n] = {
            f[0]["ext"]: f[1] for f in node_files if f[0]["node"] == n
        }
    return [
        file
        for file in (node_find_file(n, path_dict) for n in path_dict)
        if file
    ]


def edge_list_files(
    graph_dir: str,
    nodes: tuple[tuple[str, str], ...] | tuple[str, ...] | None = None,
) -> list[str]:
    """List all edge files in graph.

    If nodes is provided, only return edges between node types that are both in
    nodes list.
    """

    def edge_find_file(
        n1: str, n2: str, path_dict: dict[str, dict[str, str]]
    ) -> str:
        """Find the edge file in data_dir for the provided node types."""
        edge = edge_key(n1, n2)
        try:
            available_files = path_dict[edge]
        except KeyError:
            raise FileNotFoundError(
                f'No edge file found for nodes "{n1}", "{n2}".'
            )

        ext_preference = ["npy", "tsv", "tsv.gz", "pickle"]
        for ext in ext_preference:
            try:
                return available_files[ext]
            except KeyError:
                continue

        raise FileNotFoundError(
            f'No file found for nodes "{n1}", "{n2}" with a'
            + " supported file extension."
        )

    def edge_files_containing(
        nodes: Sequence[tuple[str, str]] | Sequence[str] | None,
        edge_files: dict[str, dict[str, str]],
    ) -> list[str]:
        r"""Find the preferred edge file for the provided nodes in data_dir.

        If nodes is "all" find a file for all nodes in the data_dir, otherwise
        only find files for nodes in the requested list. This means all edge
        files linking pairs of node types, where both node types are in the
        supplied list.

        Preferred file is based on the extension. Extension preference can be
        seen in `edge_find_file`.
        """
        assert (not nodes) or isinstance(nodes, tuple)

        if not nodes:
            edges = tuple(edge_files.keys())
        elif isinstance(nodes[0], str):
            edges = tuple(
                edge_key(n1, n2)  # type: ignore[arg-type]
                for i, n1 in enumerate(nodes)
                for n2 in nodes[i:]
                if edge_key(n1, n2) in edge_files  # type: ignore[arg-type]
            )
        else:
            edges = tuple(
                edge_key(e[0], e[1])
                for e in nodes
                if edge_key(e[0], e[1]) in edge_files
            )

        return [edge_find_file(*edge_parts(e), edge_files) for e in edges]

    files = os.listdir(graph_dir)
    edge_files = [
        (m.groupdict(), os.path.join(graph_dir, m.group()))
        for m in (re.search(EDGE_PATH_REGEX, f) for f in files)
        if m is not None
    ]
    edges = {edge_key(e[0]["n1"], e[0]["n2"]) for e in edge_files}
    path_dict: dict[str, dict[str, str]] = {}
    for e in edges:
        path_dict[e] = {
            f[0]["ext"]: f[1]
            for f in edge_files
            if edge_key(f[0]["n1"], f[0]["n2"]) == e
        }

    return edge_files_containing(nodes, path_dict)


def node_gen_id_label(name: str, namespace: str) -> str:
    return f"{name}:ID({namespace})"


def node_id_label_parts(label: str) -> tuple[str, str]:
    pattern = r"(?P<name>\w+):ID\((?P<namespace>\w+)\)"
    match = re.search(pattern, label)

    if match is None:
        raise ValueError(f"{label} does not match label naming convention.")

    name = match.groupdict()["name"]
    namespace = match.groupdict()["namespace"]

    return (name, namespace)


def edge_gen_header(start_id: str, end_id: str, features: list[str]) -> str:
    feat_header = "\t" + "\t".join(features) if features else ""

    return f":START_ID({start_id})\t:END_ID({end_id}){feat_header}"


def edge_header_parts(
    header: str,
) -> tuple[str, str, list[str], tuple[int, ...]]:
    """Parse the header for column names.

    Returns
    -------
    start_id, end_id : str
        The node namespace for the start and end of the edges.
    features : list[str]
        A (possibly empty) list of feature names.
    col_indices : tuple[int]
        The indices to sort columns into start id, end id, *features

    """
    ids = re.findall(r":((?:START)|(?:END))_ID\((\w+)\)", header)
    for idx, (position, node) in enumerate(ids):
        if position == "START":
            start_id: str = node
            start_idx = idx
        elif position == "END":
            end_id: str = node
            end_idx = idx

    features: list[str] = [
        feat
        for feat in re.findall(r"([\w:()]+)", header)
        if not (feat.startswith(":START") or feat.startswith(":END"))
    ]
    col_indices = (start_idx, end_idx) + tuple(
        i for i in range(len(features) + 2) if i not in (start_idx, end_idx)
    )

    return (start_id, end_id, features, col_indices)


def select_graph_components(
    nodes, edges, graph_dir: str
) -> tuple[list[str], list[str]]:
    """Determine which nodes and edges to select.

    If nodes and edges are both "all", return all graph saved components.

    If edges is "all" and nodes is a tuple of nodes, return all graph
    components which inclusively contain the nodes, i.e. edges where *both*
    ends of the edge are a provided node type.

    If nodes is "all" and edges is a tuple of tuples, return all edges in
    `edges` and only the nodes in the edges. If one side of an edge descriptor
    is "*" match all nodes that are in an edge with the node on the other side
    of the edge descriptor.
    """
    if (not isinstance(nodes, (str, tuple))) or (
        isinstance(nodes, str) and nodes != "all"
    ):
        raise TypeError('Nodes must be a tuple or "all"')
    if (
        (not isinstance(edges, str | tuple))
        or (isinstance(edges, str) and edges != "all")
        or (isinstance(edges, tuple) and not isinstance(edges[0], tuple))
    ):
        raise TypeError('Edges must be a tuple of tuples or "all"')

    def expand_edge(edge, files):
        n1, n2 = edge_parts(edge)
        if "*" not in (n1, n2):
            return (edge,)

        if n1 == "*":
            n1 = n2

        return tuple(
            e.groups()[0:2]
            for e in (re.search(EDGE_PATH_REGEX, f) for f in files)
            if (e is not None) and (n1 in e.groups()[0:2])
        )

    def collect_nodes(edges, files):
        # Relational nodes look like their related edges
        # ({parent_node}_{child_node}.tsv).
        all_relational_nodes = [
            m.groups()
            for m in (re.search(r"(\w*)_(\w*)_nodes.tsv", f) for f in files)
            if m is not None
        ]
        relational_nodes = {
            "_".join(m)
            for n1, n2 in edges
            for m in all_relational_nodes
            if (n1 in m) and (n2 in m)
        }
        regular_nodes = {
            n
            for e in edges
            if ("_".join(e) not in relational_nodes)
            and ("_".join(e[::-1]) not in relational_nodes)
            for n in e
        }
        return tuple(relational_nodes.union(regular_nodes))

    files = os.listdir(graph_dir)

    if edges != "all":
        edges = sum((expand_edge(e, files) for e in edges), ())

    if (nodes == "all") and (edges != "all"):
        nodes = collect_nodes(edges, files)

    if edges != "all":
        edge_files = edge_list_files(graph_dir, edges)
    elif nodes == "all":
        edge_files = edge_list_files(graph_dir)
    else:
        edge_files = edge_list_files(graph_dir, nodes)

    if nodes == "all":
        node_files = node_list_files(graph_dir)
    else:
        node_files = node_list_files(graph_dir, nodes)

    return (node_files, edge_files)

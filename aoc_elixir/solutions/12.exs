Code.require_file("lib/input.ex")
Code.require_file("lib/grid.ex")
filename = "input/12.txt"
# filename = "test_input/12.txt"
input = Input
  # .ints(filename)
  # .line_tokens(filename)
  .lines(filename)
  # .line_of_ints(filename)

defmodule Day12 do
  def make_graph(input) do
    input
      |> Enum.map(fn l -> String.split(l, "-") end)
      |> Enum.map(&List.to_tuple/1)
      |> Enum.reduce({MapSet.new(), Map.new()}, fn ({n1, n2}, {small_nodes, edges}) ->
        updated_small_nodes = cond do
          String.downcase(n1) == n1 && String.downcase(n2) == n2 -> MapSet.union(small_nodes, MapSet.new([n1, n2]))
          String.downcase(n1) == n1 -> MapSet.put(small_nodes, n1)
          String.downcase(n2) == n2 -> MapSet.put(small_nodes, n2)
          true -> small_nodes
        end

        edges = Map.update(edges, n1, MapSet.new([n2]), fn s -> MapSet.put(s, n2) end)
        edges = Map.update(edges, n2, MapSet.new([n1]), fn s -> MapSet.put(s, n1) end)

        {updated_small_nodes, edges}
      end)
  end

  def traverse_inner(curr_node, small_nodes, edges, visited_counts, neighbor_filter) do
    updated_visited_counts = cond do
      MapSet.member?(small_nodes, curr_node) -> Map.update(visited_counts, curr_node, 1, fn v -> v + 1 end)
      true -> visited_counts
    end

    valid_neighbors = Map.get(edges, curr_node, MapSet.new())
      |> Enum.filter(fn n -> neighbor_filter.(updated_visited_counts, n) end)

    valid_neighbors
      |> Enum.map(fn n -> traverse(n, small_nodes, edges, updated_visited_counts, neighbor_filter) end)
      |> Enum.sum
  end

  def traverse(curr_node, small_nodes, edges, visited_counts, neighbor_filter) do
    case curr_node do
      "end" -> 1
      _ -> traverse_inner(curr_node, small_nodes, edges, visited_counts, neighbor_filter)
    end
  end

  def p2_valid_neighbor(visited_counts, node) do
    cond do
      node == "start" -> false
      !Map.has_key?(visited_counts, node) -> true
      !Enum.any?(Map.values(visited_counts), fn v -> v == 2 end) -> true
      true -> false
    end
  end
end

{small_nodes, edges} = Day12.make_graph(input)
IO.inspect(small_nodes)
IO.inspect(edges)

part1 = Day12.traverse("start", small_nodes, edges, Map.new(), fn (counts, node) -> !Map.has_key?(counts, node) end)
part2 = Day12.traverse("start", small_nodes, edges, Map.new(), fn (counts, node) -> Day12.p2_valid_neighbor(counts, node) end)

IO.puts("Part 1: #{part1}")
IO.puts("Part 2: #{part2}")

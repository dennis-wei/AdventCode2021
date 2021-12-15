defmodule Day15 do
  def get_input() do
    filename = "input/15.txt"
    # filename = "test_input/15.txt"
    Input
      # .ints(filename)
      # .line_tokens(filename)
      .lines(filename)
      # .line_of_ints(filename)
  end

  def make_grid(input, replication_factor \\ 1) do
    base_grid = input
      |> Enum.map(&String.graphemes/1)
      |> Enum.map(fn r -> Enum.map(r, &String.to_integer/1) end)
      |> Grid.make_grid

    max_x = Map.keys(base_grid)
      |> Enum.max_by(fn {x, _y} -> x end)
      |> then(fn t -> elem(t, 0) end)
    max_y = Map.keys(base_grid)
      |> Enum.max_by(fn {_x, y} -> y end)
      |> then(fn t -> elem(t, 1) end)

    Enum.reduce(0..replication_factor-1, %{}, fn (i, acc) ->
      Enum.reduce(0..replication_factor-1, acc, fn (j, acc) ->
        Enum.reduce(base_grid, acc, fn ({{x, y}, r}, acc) ->
          nx = x + (max_x + 1) * i
          ny = y + (max_y + 1) * j

          risk = cond do
            r + i + j <= 9 -> r + i + j
            true -> r + i + j - 9
          end

          Map.put(acc, {nx, ny}, risk)
        end)
      end)
    end)
  end

  def make_graph(grid) do
    with_nodes = Graph.new
      |> Graph.add_vertices(Map.keys(grid))

    Enum.reduce(Map.keys(grid), with_nodes, fn (p1, acc) ->
      Enum.reduce(Grid.get_neighbors(grid, p1), acc, fn ({p2, n}, acc) ->
        edge = Graph.Edge.new(p1, p2, weight: n)
        acc |> Graph.add_edge(edge)
      end)
    end)
  end

  def part1() do
    input = get_input()
    grid = Day15.make_grid(input)
    graph = Day15.make_graph(grid)

    max_x = Map.keys(grid)
      |> Enum.max_by(fn {x, _y} -> x end)
      |> then(fn t -> elem(t, 0) end)
    max_y = Map.keys(grid)
      |> Enum.max_by(fn {_x, y} -> y end)
      |> then(fn t -> elem(t, 1) end)

    path = Graph.dijkstra(graph, {0, 0}, {max_x, max_y})
    part1 = Enum.reduce(tl(path), 0, fn (p, acc) -> acc + Map.get(grid, p) end)
    IO.puts("Part 1: #{part1}")
  end

  def part2() do
    input = get_input()
    grid = Day15.make_grid(input, 5)
    graph = Day15.make_graph(grid)

    max_x = Map.keys(grid)
      |> Enum.max_by(fn {x, _y} -> x end)
      |> then(fn t -> elem(t, 0) end)
    max_y = Map.keys(grid)
      |> Enum.max_by(fn {_x, y} -> y end)
      |> then(fn t -> elem(t, 1) end)

    path = Graph.dijkstra(graph, {0, 0}, {max_x, max_y})
      |> IO.inspect
    part2 = Enum.reduce(tl(path), 0, fn (p, acc) -> acc + Map.get(grid, p) end)
    IO.puts("Part 2: #{part2}")
  end

  def solve() do
    part1()
    part2()
  end
end

Day15.solve()

Code.require_file("lib/input.ex")
Code.require_file("lib/grid.ex")
filename = "input/9.txt"
# filename = "test_input/9.txt"
input = Input
  # .ints(filename)
  # .line_tokens(filename)
  .lines(filename)
  # .line_of_ints(filename)

defmodule Day9 do
  def make_grid(rows) do
    rows
      |> Enum.map(&String.trim/1)
      |> Enum.map(&String.graphemes/1)
      |> Enum.map(fn r -> Enum.map(r, &String.to_integer/1) end)
      |> Grid.make_grid
  end

  @neighbors [{0, 1}, {0, -1}, {1, 0}, {-1, 0}]
  def neighbors, do: @neighbors

  def get_neighbors(grid, {x, y}) do
    Enum.reduce(Day9.neighbors(), [], fn ({dx, dy}, acc) ->
      adj = {x + dx, y + dy}
      case Map.get(grid, adj) do
        nil -> acc
        n -> [{adj, n} | acc]
      end
    end)
  end

  def recurse_inner(grid, {{x, y}, n}, {traversed, acc}) do
    traversed = MapSet.put(traversed, {x, y})
    acc = [{{x, y}, n} | acc]

    Day9.get_neighbors(grid, {x, y})
      |> Enum.reduce({traversed, acc}, fn ({adj, nadj}, {traversed, acc}) ->
        case nadj > n && nadj != 9 do
          true -> Day9.recurse(grid, {adj, nadj}, {traversed, acc})
          false -> {traversed, acc}
        end
      end)
  end

  def recurse(grid, {{x, y}, n}, {traversed, acc}) do
    case MapSet.member?(traversed, {x, y}) do
      true -> {traversed, acc}
      false -> Day9.recurse_inner(grid, {{x, y}, n}, {traversed, acc})
    end

  end
end

grid = Day9.make_grid(input)

{part1, lps} = grid
  |> Enum.reduce({0, []}, fn ({{x, y}, n}, {p1_acc, lps}) ->
    is_lp = Day9.get_neighbors(grid, {x, y})
      |> Enum.all?(fn {_adj, nadj} -> nadj > n end)

    case is_lp do
      true -> {p1_acc + n + 1, [{{x, y}, n} | lps]}
      false -> {p1_acc, lps}
    end
  end)

basins = lps
  |> Map.new(fn {{x, y}, n} -> {{{x, y}, n}, Day9.recurse(grid, {{x, y}, n}, {MapSet.new(), []})} end)

basin_sizes = basins
  |> Map.new(fn {k, {_traversed, acc}} -> {k, length(acc)} end)

part2 = basin_sizes
  |> Map.values
  |> Enum.sort(:desc)
  |> Enum.take(3)
  |> Enum.product

IO.puts("Part 1: #{part1}")
IO.puts("Part 2: #{part2}")

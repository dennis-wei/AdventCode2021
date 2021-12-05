Code.require_file("lib/input.ex")
filename = "input/5.txt"
# filename = "test_input/5.txt"
input = Input
  # .ints(filename)
  .line_tokens(filename)
  # .lines(filename)

defmodule Day5 do
  def get_tuple_nums(t) do
    t
      |> String.split(",")
      |> Enum.map(&String.to_integer/1)
  end

  def extract_row([t1, _t2, t3]) do
    {Day5.get_tuple_nums(t1), Day5.get_tuple_nums(t3)}
  end

  def apply_vert_row(x, {y1, y2}, grid) do
    Enum.reduce(y1..y2, grid, fn (y, grid) -> Map.update(grid, {x, y}, 1, fn n -> n + 1 end) end)
  end

  def apply_hor_row({x1, x2}, y, grid) do
    Enum.reduce(x1..x2, grid, fn (x, grid) -> Map.update(grid, {x, y}, 1, fn n -> n + 1 end) end)
  end

  def apply_diag_row({x1, y1}, {x2, y2}, grid) do
    dx = if x2 > x1 do 1 else -1 end
    dy = if y2 > y1 do 1 else -1 end

    Enum.reduce(0..abs(x2 - x1), grid, fn (n, grid) ->
      Map.update(grid, {x1 + n * dx, y1 + n * dy}, 1, fn e -> e + 1 end)
    end)
  end

  def make_grid(rows, allow_diagonals \\ true) do
    rows
      |> Enum.reduce(Map.new(), fn ({[x1, y1], [x2, y2]}, grid) ->
        cond do
          x1 == x2 -> Day5.apply_vert_row(x1, {y1, y2}, grid)
          y1 == y2 -> Day5.apply_hor_row({x1, x2}, y1, grid)
          allow_diagonals -> Day5.apply_diag_row({x1, y1}, {x2, y2}, grid)
          true -> grid
        end
      end)
  end
end

parsed = input
  |> Enum.map(&Day5.extract_row/1)

part1 = Day5.make_grid(parsed, false)
  |> Map.values
  |> Enum.filter(fn n -> n > 1 end)
  |> length

part2 = Day5.make_grid(parsed, true)
  |> Map.values
  |> Enum.filter(fn n -> n > 1 end)
  |> length

IO.puts("Part 1: #{part1}")
IO.puts("Part 2: #{part2}")

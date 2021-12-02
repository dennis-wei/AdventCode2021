Code.require_file("lib/input.ex")
filename = "input/2.txt"
# filename = "test_input/2.txt"
input = Input
  # .ints(filename)
  .line_tokens(filename)
  |> Enum.map(&List.to_tuple/1)
  |> Enum.map(fn {dir, n} -> {dir, String.to_integer(n)} end)

defmodule Day2 do
  def apply_row_part1(row, {x, y}) do
    case row do
      {"forward", n} -> {x + n, y}
      {"up", n} -> {x, y - n}
      {"down", n} -> {x, y + n}
      {_, _} -> {x, y}
    end
  end

  def apply_row_part2(row, {x, y, aim}) do
    case row do
      {"forward", n} -> {x + n, y + n * aim, aim}
      {"up", n} -> {x, y, aim - n}
      {"down", n} -> {x, y, aim + n}
      {_, _} -> {x, y, aim}
    end
  end
end

part1 = input
  |> Enum.reduce({0, 0}, fn (row, acc) -> Day2.apply_row_part1(row, acc) end)
  |> then(fn {x, y} -> x * y end)

part2 = input
  |> Enum.reduce({0, 0, 0}, fn (row, acc) -> Day2.apply_row_part2(row, acc) end)
  |> then(fn {x, y, _aim} -> x * y end)

IO.puts("Part 1: #{part1}")
IO.puts("Part 2: #{part2}")

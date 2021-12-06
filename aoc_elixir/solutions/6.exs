Code.require_file("lib/input.ex")
filename = "input/6.txt"
# filename = "test_input/6.txt"
input = Input
  # .ints(filename)
  # .line_tokens(filename)
  # .lines(filename)
  .line_of_ints(filename)

defmodule Day6 do
end

counts = input
  |> Enum.reduce(%{}, fn (n, map) -> Map.update(map, n, 1, fn n -> n + 1 end) end)

as_list = 0..8
  |> Enum.map(fn n -> Map.get(counts, n, 0) end)
  |> IO.inspect

part1 = 1..80
  |> Enum.reduce(as_list, fn (_n, l) ->
    [head | tail] = l
    List.update_at(tail ++ [head], 6, fn n -> n + head end)
  end)
  |> Enum.sum

part2 = 1..256
  |> Enum.reduce(as_list, fn (_n, l) ->
    [head | tail] = l
    List.update_at(tail ++ [head], 6, fn n -> n + head end)
  end)
  |> Enum.sum

IO.puts("Part 1: #{part1}")
IO.puts("Part 2: #{part2}")

Code.require_file("lib/input.ex")
Code.require_file("lib/grid.ex")
filename = "input/14.txt"
# filename = "test_input/14.txt"
input = Input
  # .ints(filename)
  .line_tokens(filename, "\n", "\n\n")
  # .lines(filename)
  # .line_of_ints(filename)

defmodule Day14 do
  def iter(acc, instr_map) do
    Enum.reduce(acc, %{}, fn ({t, v}, acc) ->
      {p1, p2} = Map.get(instr_map, t)

      acc
        |> Map.update(p1, v, fn n -> n + v end)
        |> Map.update(p2, v, fn n -> n + v end)
    end)
  end

  def solve(start, instr_map, num_iters) do
    initial_map = Enum.zip(String.graphemes(start), tl(String.graphemes(start)))
      |> Enum.reduce(%{}, fn (t, acc) -> Map.update(acc, elem(t, 0) <> elem(t, 1), 1, fn v -> v + 1 end) end)

    solved_pairs = Enum.reduce(0..num_iters-1, initial_map, fn (_n, acc) -> iter(acc, instr_map) end)
    char_counts = solved_pairs
      |> Enum.reduce(%{}, fn ({k, v}, acc) ->
        Map.update(acc, String.at(k, 0), v, fn n -> n + v end)
      end)

    char_counts = Map.update(char_counts, String.at(start, String.length(start)-1), 1, fn n -> n + 1 end)

    most = Enum.max_by(char_counts, fn {_k, v} -> v end)
      |> elem(1)
    least = Enum.min_by(char_counts, fn {_k, v} -> v end)
      |> elem(1)

    most - least
  end
end

{starting_code, instructions} = List.to_tuple(input)
starting_code = hd(starting_code)

instr_map = Enum.reduce(instructions, %{}, fn (row, acc) ->
  {pair, c} = row
    |> String.split(" -> ")
    |> List.to_tuple

  p1 = String.at(pair, 0) <> c
  p2 = c <> String.at(pair, 1)

  Map.put(acc, pair, {p1, p2})
end)

Day14.solve(starting_code, instr_map, 1)

part1 = Day14.solve(starting_code, instr_map, 10)
part2 = Day14.solve(starting_code, instr_map, 40)

IO.puts("Part 1: #{part1}")
IO.puts("Part 2: #{part2}")

Code.require_file("lib/input.ex")
filename = "input/8.txt"
# filename = "test_input/8.txt"
input = Input
  # .ints(filename)
  .line_tokens(filename, " | ", "\n")
  # .lines(filename)
  # .line_of_ints(filename)

defmodule Day8 do
  def permutations([]), do: [[]]
  def permutations(list), do: for elem <- list, rest <- permutations(list--[elem]), do: [elem|rest]

  @segment_mapping Map.new([
    {"123567", 0},
    {"36", 1},
    {"23457", 2},
    {"23467", 3},
    {"1346", 4},
    {"12467", 5},
    {"124567", 6},
    {"236", 7},
    {"1234567", 8},
    {"123467", 9}
  ])
  def segment_mapping, do: @segment_mapping

  def to_key(str, mapping) do
    String.graphemes(str)
      |> Enum.map(fn c -> Map.get(mapping, c) end)
      |> Enum.sort
      |> Enum.map(fn n ->
        Integer.to_string(n)
      end)
      |> then(fn ilist -> Enum.join(ilist, "") end)
  end

  def is_mapping_valid(signal, mapping) do
    signal
      |> Enum.all?(fn str ->
        Map.has_key?(Day8.segment_mapping, Day8.to_key(str, mapping))
      end)
  end

  def apply_mapping(mapping, o) do
    Map.get(Day8.segment_mapping, Day8.to_key(o, mapping))
  end

  def compute({signal, output}) do
    {result, mapping} = Day8.permutations(String.graphemes("abcdefg"))
      |> Enum.reduce_while({:cont, %{}}, fn (corder, _acc) ->
        mapping = Enum.zip(corder, [1, 2, 3, 4, 5, 6, 7])
          |> Map.new()

        case Day8.is_mapping_valid(signal, mapping) do
          true -> {:halt, {:valid, mapping}}
          false -> {:cont, {:invalid, %{}}}
        end
      end)

    case result do
      :valid ->
        Enum.map(output, fn str -> apply_mapping(mapping, str) end)
          |> Enum.map(&Integer.to_string/1)
          |> then(fn ilist -> Enum.join(ilist, "") end)
          |> String.to_integer
      :invalid ->
        IO.puts("no valid mapping found")
        0
    end
  end
end

input = input
  |> Enum.map(&List.to_tuple/1)
  |> Enum.map(fn {signal, output} ->
    {String.split(signal, " "), String.split(output, " ")}
  end)

easy_sizes = MapSet.new([2, 3, 4, 7])
part1 = input
  |> Enum.map(fn {_signal, output} -> output end)
  |> Enum.map(fn output -> Enum.count(output, fn s ->
    MapSet.member?(easy_sizes, String.length(s))
  end) end)
  |> Enum.sum

part2 = input
  |> Enum.map(fn {signal, output} -> Day8.compute({signal, output}) end)
  |> Enum.sum

IO.puts("Part 1: #{part1}")
IO.puts("Part 2: #{part2}")

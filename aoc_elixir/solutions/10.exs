Code.require_file("lib/input.ex")
filename = "input/10.txt"
# filename = "test_input/10.txt"
input = Input
  # .ints(filename)
  # .line_tokens(filename)
  .lines(filename)

defmodule Day10 do
  @p1_points %{
    ")" => 3,
    "]" => 57,
    "}" => 1197,
    ">" => 25137,
  }
  def p1_points, do: @p1_points

  @p2_points %{
    "(" => 1,
    "[" => 2,
    "{" => 3,
    "<" => 4,
  }
  def p2_points, do: @p2_points

  def matches(c1, c2) do
    c1 == "(" && c2 == ")" ||
      c1 == "[" && c2 == "]" ||
      c1 == "{" && c2 == "}" ||
      c1 == "<" && c2 == ">"
  end

  def p1_line(line) do
    line
      |> String.graphemes
      |> Enum.reduce_while({:valid, []}, fn (c, {_status, acc}) ->
        case Map.has_key?(Day10.p2_points, c) do
          true -> {:cont, {:valid, [c | acc]}}
          false -> case matches(hd(acc), c) do
            true -> {:cont, {:valid, tl(acc)}}
            false -> {:halt, {:corrupted, c}}
          end
        end
      end)
  end

  def p2_score(acc) do
    acc
      |> Enum.reduce(0, fn (c, acc) -> acc * 5 + Map.get(Day10.p2_points, c) end)
  end
end

mapped = input
  |> Enum.map(fn l -> Day10.p1_line(l) end)

part1 = mapped
  |> Enum.filter(fn {status, _} -> status == :corrupted end)
  |> Enum.map(fn {_, c} -> Map.get(Day10.p1_points, c) end)
  |> Enum.sum

part2_scores = mapped
  |> Enum.filter(fn {status, _} -> status == :valid end)
  |> Enum.map(fn {_, acc} -> Day10.p2_score(acc) end)
  |> Enum.sort

middle_element = :math.floor(length(part2_scores) / 2)
  |> trunc
part2 = Enum.at(part2_scores, middle_element)

IO.puts("Part 1: #{part1}")
IO.puts("Part 2: #{part2}")

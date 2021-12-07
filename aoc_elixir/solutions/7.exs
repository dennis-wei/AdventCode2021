Code.require_file("lib/input.ex")
filename = "input/7.txt"
# filename = "test_input/7.txt"
input = Input
  # .ints(filename)
  # .line_tokens(filename)
  # .lines(filename)
  .line_of_ints(filename)

defmodule Day7 do
  def sq_sum(n) do
    n * (n + 1) / 2
  end
end

imin = Enum.min(input)
imax = Enum.max(input)

part1 = imin..imax
  |> Enum.reduce(-1, fn (n, acc) ->
    res = Enum.reduce(input, 0, fn (m, acc) -> acc + abs(n - m) end)
    case acc do
      -1 -> res
      prior -> min(prior, res)
    end
  end)

part2 = imin..imax
  |> Enum.reduce(-1, fn (n, acc) ->
    res = Enum.reduce(input, 0, fn (m, acc) -> acc + Day7.sq_sum(abs(n - m)) end)
    case acc do
      -1 -> res
      prior -> min(prior, res)
    end
  end)

IO.puts("Part 1: #{part1}")
IO.puts("Part 2: #{part2}")

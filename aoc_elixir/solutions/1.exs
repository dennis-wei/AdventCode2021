Code.require_file("lib/input.ex")
input = Input
  .ints("input/1.txt")

tail = Enum.drop(input, 1)
part1_zipped = Enum.zip(input, tail)

part1 = part1_zipped
  |> Enum.map(fn {n1, n2} -> n2 > n1 end)
  |> Enum.map(fn b -> if b do 1 else 0 end end)
  |> Enum.sum

drop3 = Enum.drop(input, 3)
part2_zipped = Enum.zip(input, drop3)
part2 = part2_zipped
  |> Enum.map(fn {n1, n2} -> n2 > n1 end)
  |> Enum.map(fn b -> if b do 1 else 0 end end)
  |> Enum.sum

IO.puts("Part 1: #{part1}")
IO.puts("Part 2: #{part2}")

Code.require_file("lib/input.ex")
Code.require_file("lib/grid.ex")
filename = "input/17.txt"
# filename = "test_input/17.txt"
input = Input
  .read_file(filename)
  # .ints(filename)
  # .line_tokens(filename)
  # .lines(filename)
  # .line_of_ints(filename)

defmodule Day17 do
  def parse_input(input) do
    tokens = String.split(input, " ")
    {x1, x2} = Enum.at(tokens, 2)
      |> String.replace("x=", "")
      |> String.replace(",", "")
      |> String.split("..")
      |> Enum.map(&String.to_integer/1)
      |> List.to_tuple()

    {lx, hx} = cond do
      x1 > x2 -> {x2, x1}
      true -> {x1, x2}
    end

    {y1, y2} = Enum.at(tokens, 3)
      |> String.replace("y=", "")
      |> String.split("..")
      |> Enum.map(&String.to_integer/1)
      |> List.to_tuple()

    {ly, hy} = cond do
      y1 > y2 -> {y2, y1}
      true -> {y1, y2}
    end

    {{lx, hx}, {ly, hy}}
  end

  def simulate(target, hax, ly, ix, iy) do
    x = 0
    y = 0
    vx = ix
    vy = iy
    Enum.reduce_while(0..999999, {:miss, x, y, vx, vy, 0}, fn (_n, {_status, x, y, vx, vy, my}) ->
      nx = x + vx
      ny = y + vy

      nmy = cond do
        ny > my -> ny
        true -> my
      end

      nvx = cond do
        vx == 0 -> 0
        vx < 0 -> vx + 1
        vx > 0 -> vx - 1
      end

      nvy = vy - 1

      cond do
        MapSet.member?(target, {nx, ny}) -> {:halt, {:hit, nx, ny, nvx, nvy, nmy}}
        abs(nx) > hax -> {:halt, {:miss, nx, ny, nvx, nvy, nmy}}
        ny < ly -> {:halt, {:miss, nx, ny, nvx, nvy, nmy}}
        true -> {:cont, {:miss, nx, ny, nvx, nvy, nmy}}
      end
    end)
  end

  def make_target_set({{lx, hx}, {ly, hy}}) do
    Enum.reduce(lx..hx, MapSet.new(), fn (x, acc) ->
      Enum.reduce(ly..hy, acc, fn (y, acc) ->
        MapSet.put(acc, {x, y})
      end)
    end)
  end

  def brute_force(input) do
    {{lx, hx}, {ly, hy}} = parse_input(input)
    target = make_target_set({{lx, hx}, {ly, hy}})
    hax = Enum.max([abs(lx), abs(hx)])

    Enum.reduce(0..hax, {0, 0}, fn (x, {num_hit, highest_y}) ->
      Enum.reduce(-abs(ly)-1..abs(ly)+1, {num_hit, highest_y}, fn (y, {num_hit, highest_y}) ->
        {status, _nx, _ny, _vx, _vy, my} = simulate(target, hax, ly, x, y)

        case status do
          :hit -> cond do
            my > highest_y -> {num_hit + 1, my}
            true -> {num_hit + 1, highest_y}
          end
          :miss -> {num_hit, highest_y}
        end
      end)
    end)
  end
end

{part2, part1} = Day17.brute_force(input |> String.trim)

IO.puts("Part 1: #{part1}")
IO.puts("Part 2: #{part2}")

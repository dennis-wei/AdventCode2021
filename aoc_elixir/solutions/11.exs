Code.require_file("lib/input.ex")
Code.require_file("lib/grid.ex")
filename = "input/11.txt"
# filename = "test_input/11.txt"
input = Input
  # .ints(filename)
  .lines(filename)
  # .line_tokens(filename)
  # .line_of_ints(filename)

defmodule Day11 do
  def simul(grid) do
    grid = Map.new(grid, fn {k, v} -> {k, v + 1} end)
    recur_flash(grid, [], MapSet.new())
  end

  def recur_flash(grid, will_flash, flashed) do
    grid_post_flash = will_flash
      |> Enum.reduce(grid, fn (p, acc) -> Map.put(acc, p, 0) end)
    updated_flashed = MapSet.union(flashed, MapSet.new(will_flash))

    neighbor_grid_update = will_flash
      |> Enum.reduce(grid_post_flash, fn (p, acc) ->
        neighbors_to_update = Grid.get_neighbors(grid_post_flash, p, true)
          |> Enum.filter(fn {n, _v} -> !MapSet.member?(updated_flashed, n) end)
        Enum.reduce(neighbors_to_update, acc, fn ({n, _v}, acc_inner) -> Map.update!(acc_inner, n, fn v -> v + 1 end) end)
      end)

    will_flash_next = neighbor_grid_update
      |> Enum.filter(fn {_k, v} -> v > 9 end)
      |> Enum.map(fn {k, _v} -> k end)

    cond do
      Enum.empty?(will_flash_next) -> {neighbor_grid_update, length(MapSet.to_list(updated_flashed))}
      true -> recur_flash(neighbor_grid_update, will_flash_next, updated_flashed)
    end
  end

  def solve(grid, grid_size, iter \\ 1, p1_acc \\ 0) do
    {updated_grid, num_flashed} = simul(grid)
    updated_p1_acc = cond do
      iter <= 100 -> p1_acc + num_flashed
      true -> p1_acc
    end

    cond do
      num_flashed == grid_size -> {p1_acc, iter}
      true -> solve(updated_grid, grid_size, iter + 1, updated_p1_acc)
    end
  end
end

grid = input
  |> Enum.map(&String.graphemes/1)
  |> Enum.map(fn r -> Enum.map(r, &String.to_integer/1) end)
  |> Grid.make_grid

IO.puts("initial grid")
Grid.print_grid(grid)

{part1, part2} = Day11.solve(grid, length(Map.to_list(grid)))

IO.puts("Part 1: #{part1}")
IO.puts("Part 2: #{part2}")

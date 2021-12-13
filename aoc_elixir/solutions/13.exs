Code.require_file("lib/input.ex")
Code.require_file("lib/grid.ex")
filename = "input/13.txt"
# filename = "test_input/13.txt"
input = Input
  # .ints(filename)
  .line_tokens(filename, "\n", "\n\n")
  # .lines(filename)
  # .line_of_ints(filename)

defmodule Day13 do
  def make_grid(input) do
    points = input
      |> Enum.map(fn l -> String.split(l, ",") end)
      |> Enum.map(&List.to_tuple/1)
      |> Enum.map(fn {x, y} -> {String.to_integer(x), String.to_integer(y)} end)
      |> MapSet.new

    max_x = points
      |> Enum.map(fn {x, _y} -> x end)
      |> Enum.max

    max_y = points
      |> Enum.map(fn {_x, y} -> y end)
      |> Enum.max

    Enum.reduce(0..max_x, Map.new(), fn (x, acc) ->
      Enum.reduce(0..max_y, acc, fn (y, acc) ->
        case MapSet.member?(points, {x, y}) do
          true -> Map.put(acc, {x, y}, "#")
          false -> Map.put(acc, {x, y}, ".")
        end
      end)
    end)
  end

  def get_grid_bounds(grid) do
    min_x = Map.keys(grid)
      |> Enum.map(fn {x, _y} -> x end)
      |> Enum.min
    max_x = Map.keys(grid)
      |> Enum.map(fn {x, _y} -> x end)
      |> Enum.max

    min_y = Map.keys(grid)
      |> Enum.map(fn {_x, y} -> y end)
      |> Enum.min
    max_y = Map.keys(grid)
      |> Enum.map(fn {_x, y} -> y end)
      |> Enum.max

    {{min_x, max_x}, {min_y, max_y}}
  end

  def print_grid(grid) do
    {{min_x, max_x}, {min_y, max_y}} = get_grid_bounds(grid)

    Enum.each(min_y..max_y, fn y ->
      Enum.reduce(min_x..max_x, "", fn (x, acc) -> "#{acc}#{Map.get(grid, {x, y})}" end)
        |> IO.puts
    end)
  end

  def do_fold(fold, grid) do
    {axis, n} = fold
      |> String.replace("fold along ", "")
      |> String.split("=")
      |> List.to_tuple

    case axis do
      "x" -> do_x_fold(String.to_integer(n), grid)
      "y" -> do_y_fold(String.to_integer(n), grid)
      _ -> raise "invalid axis"
    end
  end

  def do_y_fold(n, grid) do
    {{min_x, max_x}, {_min_y, max_y}} = get_grid_bounds(grid)

    Enum.reduce(0..(max_y-n), grid, fn (offset, acc) ->
      Enum.reduce(min_x..max_x, acc, fn (x, acc) ->
        higher = Map.get(grid, {x, n - offset})
        lower = Map.get(grid, {x, n + offset})

        cond do
          higher == "." && lower == "." ->
            Map.put(acc, {x, n - offset}, ".")
              |> Map.delete({x, n + offset})
          higher == "#" || lower == "#" ->
            Map.put(acc, {x, n - offset}, "#")
              |> Map.delete({x, n + offset})
          true -> raise "invalid state"
        end
      end)
    end)
  end

  def do_x_fold(n, grid) do
    {{_min_x, max_x}, {min_y, max_y}} = get_grid_bounds(grid)

    Enum.reduce(0..(max_x-n), grid, fn (offset, acc) ->
      Enum.reduce(min_y..max_y, acc, fn (y, acc) ->
        left = Map.get(grid, {n - offset, y})
        right = Map.get(grid, {n + offset, y})

        cond do
          left == "." && right == "." ->
            Map.put(acc, {n - offset, y}, ".")
              |> Map.delete({n + offset, y})
          left == "#" || right == "#" ->
            Map.put(acc, {n - offset, y}, "#")
              |> Map.delete({n + offset, y})
          true -> raise "invalid state"
        end
      end)
    end)
  end
end

{points, folds} = List.to_tuple(input)
grid = Day13.make_grid(points)
# IO.puts("initial")
# Day13.print_grid(grid)
# IO.puts("")

[first_fold | other_folds] = folds
after_first = Day13.do_fold(first_fold, grid)
# IO.puts("after first")
# Day13.print_grid(after_first)
# IO.puts("")

part1 = Map.values(after_first)
  |> Enum.count(fn c -> c == "#" end)

after_all_folds = Enum.reduce(other_folds, after_first, fn (fold, acc) ->
  Day13.do_fold(fold, acc)
end)

IO.puts("after all")
Day13.print_grid(after_all_folds)
IO.puts("")

part2 = nil

IO.puts("Part 1: #{part1}")
IO.puts("Part 2: #{part2}")

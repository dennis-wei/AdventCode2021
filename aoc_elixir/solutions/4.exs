Code.require_file("lib/input.ex")
filename = "input/4.txt"
# filename = "test_input/4.txt"
input = Input
  # .ints(filename)
  # .line_tokens(filename)
  .line_tokens(filename, "\n", "\n\n")
  # .lines(filename)

defmodule Day4 do
  def invert(glist) do
    Map.new(glist, fn ent ->
      {n, r, c} = ent
      {n, {r, c}}
    end)
  end

  def make_grid(ginput) do
    as_list = ginput
      |> Enum.map(&String.trim/1)
      |> Enum.map(fn s -> String.replace(s, "  ", " ") end)
      |> Enum.map(fn s -> String.split(s, " ") end)
      |> Enum.map(fn r -> Enum.map(r, &String.to_integer/1) end)
      |> Enum.map(&Enum.with_index/1)
      |> then(&Enum.with_index/1)
      |> Enum.flat_map(fn {row, ridx} -> Enum.map(row, fn e -> Tuple.insert_at(e, 1, ridx) end) end)

    sum = as_list
      |> Enum.map(fn e -> elem(e, 0) end)
      |> Enum.sum

    invert = invert(as_list)

    {invert, sum, 0, %{}, %{}}
  end

  def parse_input(input) do
    [raw_calls | raw_grids] = input
    calls = List.first(raw_calls)
      |> String.split(",")
      |> Enum.map(&String.to_integer/1)

    grids = raw_grids
      |> Enum.map(&Day4.make_grid/1)

    {calls, grids}
  end

  def apply_call({igrid, sum, called_sum, rmarked, cmarked}, call) do
    case Map.get(igrid, call) do
      nil -> {igrid, sum, called_sum, rmarked, cmarked}
      {ridx, cidx} -> {
        igrid, sum, called_sum + call,
        Map.update(rmarked, ridx, 1, fn n -> n + 1 end),
        Map.update(cmarked, cidx, 1, fn n -> n + 1 end),
      }
    end
  end

  def has_won(marked) do
    Map.values(marked)
      |> Enum.member?(5)
  end

  def apply_call_check_win(grid, call) do
    applied = apply_call(grid, call)
    {_igrid, sum, called_sum, rmarked, cmarked} = applied
    case has_won(rmarked) || has_won(cmarked) do
      true -> {:win, call * (sum - called_sum), applied}
      false -> {:no_win, nil, applied}
    end
  end
end

{calls, grids} = Day4.parse_input(input)
grid_tracker = grids
  |> Enum.map(fn grid ->
    {grid, nil, nil}
  end)

winning_grids = calls
  |> Enum.with_index
  |> Enum.reduce(grid_tracker, fn ({call, turn}, tracker) ->
    tracker
      |> Enum.map(fn grid_data ->
        case grid_data do
          {grid, nil, nil} -> case Day4.apply_call_check_win(grid, call) do
            {:win, winning_score, _updated_grid} -> {:finished, winning_score, turn}
            {:no_win, _, updated_grid} -> {updated_grid, nil, nil}
          end
          {:finished, score, turn} -> {:finished, score, turn}
        end
      end)
    end)

part1 = Enum.min_by(winning_grids, fn {_result, _score, turns} -> turns end)
  |> then(fn {_result, score, _turns} -> score end)

part2 = Enum.max_by(winning_grids, fn {_result, _score, turns} -> turns end)
  |> then(fn {_result, score, _turns} -> score end)

IO.puts("Part 1: #{part1}")
IO.puts("Part 2: #{part2}")

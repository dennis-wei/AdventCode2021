defmodule Grid do
  def to_map(glist) do
    Map.new(glist, fn ent ->
      {n, r, c} = ent
      {{r, c}, n}
    end)
  end

  def make_grid(rows) do
    as_list = rows
      |> Enum.map(&Enum.with_index/1)
      |> then(&Enum.with_index/1)
      |> Enum.flat_map(fn {row, ridx} -> Enum.map(row, fn e -> Tuple.insert_at(e, 1, ridx) end) end)

    to_map(as_list)
  end

  @neighbors [{0, 1}, {0, -1}, {1, 0}, {-1, 0}]
  @neighbors_diag [{0, 1}, {0, -1}, {1, 0}, {-1, 0}, {1, 1}, {1, -1}, {-1, 1}, {-1, -1}]
  def neighbors(diagonal \\ false) do
    case diagonal do
      false -> @neighbors
      true -> @neighbors_diag
    end
  end

  def get_neighbors(grid, {x, y}, diagonal \\ false) do
    Enum.reduce(neighbors(diagonal), %{}, fn ({dx, dy}, acc) ->
      adj = {x + dx, y + dy}
      case Map.get(grid, adj) do
        nil -> acc
        n -> Map.put(acc, adj, n)
      end
    end)
  end
end

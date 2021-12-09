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
end

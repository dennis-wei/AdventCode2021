Code.require_file("lib/input.ex")
filename = "input/3.txt"
# filename = "test_input/3.txt"
input = Input
  # .ints(filename)
  # .line_tokens(filename)
  .lines(filename)

defmodule Day3 do
  def ogr_filter(input, index) do
    keep = input
      |> Enum.reduce(0, fn (row, acc) ->
          if String.at(row, index) == "1" do acc + 1 else acc - 1 end
        end)
      |> then(fn c ->
          if c >= 0 do "1" else "0" end
        end)

    Enum.filter(input, fn row -> String.at(row, index) == keep end)
  end

  def csr_filter(input, index) do
    keep = input
      |> Enum.reduce(0, fn (row, acc) ->
          if String.at(row, index) == "1" do acc + 1 else acc - 1 end
        end)
      |> then(fn c ->
          if c < 0 do "1" else "0" end
        end)

    Enum.filter(input, fn row -> String.at(row, index) == keep end)
  end

  def is_singleton(input) do
    input
      |> tl
      |> Enum.empty?
  end
end

bit_size = List.first(input)
  |> String.length

acc = Map.new(0..bit_size-1, fn n -> {n, 0} end)

counts = input
  |> Enum.reduce(acc, fn (row, acc) ->
    char_list_tuples = row
      |> String.graphemes
      |> Enum.with_index

    Enum.reduce(char_list_tuples, acc, fn ({ch, idx}, acc) ->
      Map.update(acc, idx, 0, fn c ->
        if ch == "1" do c + 1 else c - 1 end
      end)
    end)
  end)
  |> Map.to_list
  |> Enum.map(fn {_idx, cnt} -> if cnt < 0 do 0 else 1 end end)

gamma = counts
  |> Enum.join
  |> String.to_integer(2)
  |> IO.inspect(label: "gamma: ")

epsilon = counts
  |> Enum.map(fn n -> if n == 0 do 1 else 0 end end)
  |> Enum.join
  |> String.to_integer(2)
  |> IO.inspect(label: "epsilon: ")

part1 = gamma * epsilon

ogr = 0..bit_size-1
  |> Enum.reduce(input, fn (idx, acc) ->
      if Day3.is_singleton(acc) do acc else Day3.ogr_filter(acc, idx) end
    end)
  |> List.first
  |> String.to_integer(2)
  |> IO.inspect(label: "ogr: ")

csr = 0..bit_size-1
  |> Enum.reduce(input, fn (idx, acc) ->
      if Day3.is_singleton(acc) do acc else Day3.csr_filter(acc, idx) end
    end)
  |> List.first
  |> String.to_integer(2)
  |> IO.inspect(label: "csr: ")

part2 = ogr * csr

IO.puts("Part 1: #{part1}")
IO.puts("Part 2: #{part2}")

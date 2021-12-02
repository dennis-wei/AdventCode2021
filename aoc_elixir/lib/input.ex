defmodule Input do
  @moduledoc """
  Documentation for AocElixir.
  """

  @doc """
  Hello world.

  ## Examples

      iex> AocElixir.hello
      :world

  """
  def read_file(filename) do
    {:ok, input} = File.read(filename)
    input
  end

  def lines(filename) do
    read_file(filename)
      |> String.trim
      |> String.split("\n")
  end

  def line_tokens(filename, sep \\ " ") do
    lines(filename)
      |> Enum.map(fn r -> String.split(r, sep) end)
  end

  def ints(filename) do
    lines(filename)
      |> Enum.map(&String.to_integer/1)
  end
end

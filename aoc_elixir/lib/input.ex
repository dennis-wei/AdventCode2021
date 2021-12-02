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
end

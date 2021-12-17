Code.require_file("lib/input.ex")
Code.require_file("lib/grid.ex")
filename = "input/16.txt"
test_filename = "test_input/16.txt"
input = Input
  .read_file(filename) |> String.trim
  # .ints(filename)
  # .line_tokens(filename)
  # .lines(filename)
  # .line_of_ints(filename)

defmodule Day16 do
  @mapping %{
    "0" => "0000",
    "1" => "0001",
    "2" => "0010",
    "3" => "0011",
    "4" => "0100",
    "5" => "0101",
    "6" => "0110",
    "7" => "0111",
    "8" => "1000",
    "9" => "1001",
    "A" => "1010",
    "B" => "1011",
    "C" => "1100",
    "D" => "1101",
    "E" => "1110",
    "F" => "1111"
  }
  def mapping, do: @mapping

  def parse_input(raw_input) do
    raw_input
      |> String.graphemes
      |> Enum.reduce("", fn (c, acc) -> acc <> Map.get(Day16.mapping, c) end)
      |> String.graphemes
  end

  def get_next_packet(input) do
    cond do
      Enum.all?(input, fn c -> c == "0" end) -> {[], ""}
      input == "" -> {[], ""}
      true -> get_next_packet_inner(input)
    end
  end

  def get_next_packet_inner(input) do
    {packet_version_bits, remaining} = Enum.split(input, 3)
    {packet_type_bits, remaining} = Enum.split(remaining, 3)

    packet_version = packet_version_bits
      |> Enum.join
      |> then(fn s -> String.to_integer(s, 2) end)
    packet_type = packet_type_bits
      |> Enum.join
      |> then(fn s -> String.to_integer(s, 2) end)

    case packet_type do
      4 -> handle_literal_packet(packet_version, remaining)
      _ -> case hd(remaining) do
        "0" -> handle_length_packet(packet_type, packet_version, tl(remaining))
        "1" -> handle_num_packet(packet_type, packet_version, tl(remaining))
      end
    end
  end

  def handle_literal_packet(version, input) do
    {num_taken, _leftover, acc} = Enum.reduce_while(input, {0, "", ""}, fn (c, {num_taken, chunk, acc}) ->
      updated_chunk = chunk <> c
      cond do
        rem(String.length(updated_chunk), 5) == 0 ->
          {bit, literal} = String.split_at(updated_chunk, 1)
          case bit do
            "1" -> {:cont, {num_taken + 1, "", acc <> literal}}
            "0" -> {:halt, {num_taken + 1 , "", acc <> literal}}
          end
        true -> {:cont, {num_taken + 1, updated_chunk, acc}}
      end
    end)

    {_removed, remaining} = Enum.split(input, num_taken)
    {[{version, String.to_integer(acc, 2)}], remaining}
  end

  def handle_length_packet(type, version, input) do
    {total_length_bits, remaining} = Enum.split(input, 15)
    total_length = total_length_bits
      |> Enum.join
      |> then(fn s -> String.to_integer(s, 2) end)
    {segment, remaining} = Enum.split(remaining, total_length)

    segment_remaining = segment
    acc = [{version, type}]
    {final_op, _segment_remaining} = Enum.reduce_while(0..10000, {acc, segment_remaining}, fn (_n, {acc, segment_remaining}) ->
      {packet, segment_remaining} = get_next_packet(segment_remaining)
      updated_acc = acc ++ packet

      cond do
        Enum.empty?(segment_remaining) ->
          {:halt, {updated_acc, segment_remaining}}
        true -> {:cont, {updated_acc, segment_remaining}}
      end
    end)

    {op_reduce(final_op), remaining}
  end

  def handle_num_packet(type, version, input) do
    {num_sub_packets_bits, remaining} = Enum.split(input, 11)
    num_sub_packets = num_sub_packets_bits
      |> Enum.join
      |> then(fn s -> String.to_integer(s, 2) end)

    acc = [{version, type}]
    {final_op, remaining} = Enum.reduce(1..num_sub_packets, {acc, remaining}, fn (_n, {acc, remaining}) ->
      {packet, remaining} = get_next_packet(remaining)
      updated_acc = acc ++ packet
      {updated_acc, remaining}
    end)

    {op_reduce(final_op), remaining}
  end

  def op_reduce(op_arr) do
    version_sum = op_arr
      |> Enum.map(fn t -> elem(t, 0) end)
      |> Enum.sum

    {_version, type} = hd(op_arr)
    args = tl(op_arr)
      |> Enum.map(fn t -> elem(t, 1) end)

    res = case type do
      0 -> Enum.sum(args)
      1 -> Enum.product(args)
      2 -> Enum.min(args)
      3 -> Enum.max(args)
      5 -> if Enum.at(args, 0) > Enum.at(args, 1), do: 1, else: 0
      6 -> if Enum.at(args, 0) < Enum.at(args, 1), do: 1, else: 0
      7 -> if Enum.at(args, 0) == Enum.at(args, 1), do: 1, else: 0
    end

    [{version_sum, res}]
  end
end

as_bit_string = Day16.parse_input(input)
{solved, _remaining} = Day16.get_next_packet(as_bit_string)

{part1, part2} = hd(solved)

IO.puts("Part 1: #{part1}")
IO.puts("Part 2: #{part2}")

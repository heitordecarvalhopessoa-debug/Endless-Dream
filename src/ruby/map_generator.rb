puts "=== ADVANCED MAZE GENERATOR ==="

width = 17
height = 13
density = 0.25
map = []

height.times do |y|
  line = "["
  width.times do |x|
    if x == 0 || x == width - 1 || y == 0 || y == height - 1
      line += "1, "
    elsif x == 1 && y == 1
      line += "4, "
    else
      line += (rand < density ? "1, " : "_, ")
    end
  end
  line.chomp!(", ")
  line += "],"
  map << line
end

puts "\nGenerated Maze Matrix:"
puts "-----------------------------------"
map.each { |l| puts l }
puts "-----------------------------------"
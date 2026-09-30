require 'find'
require 'pathname'

puts "=== Advanced Project Analyzer ==="
total_lines = 0
total_code_lines = 0
total_comment_lines = 0
total_files = 0

project_root = File.expand_path('../..', __dir__)

Find.find(project_root) do |path|
    if path.end_with?('.py', '.rb') && !path.include?('backups')
        total_files += 1
        lines = File.readlines(path)
        file_lines = lines.count
        code_lines = lines.count { |l| l.strip !~ /^(#|\/\/|\s*$)/ }
        comment_lines = lines.count { |l| l.strip =~ /^#/ }
        
        total_lines += file_lines
        total_code_lines += code_lines
        total_comment_lines += comment_lines
        
        relative_name = Pathname.new(path).relative_path_from(Pathname.new(project_root))
        puts "File: #{relative_name} -> Total: #{file_lines} | Code: #{code_lines} | Comments: #{comment_lines}"
    end
end

puts "-----------------------------------"
puts "Total Files: #{total_files}"
puts "Total Lines: #{total_lines}"
puts "Pure Code Lines: #{total_code_lines}"
puts "Comment Lines: #{total_comment_lines}"
puts "==================================="
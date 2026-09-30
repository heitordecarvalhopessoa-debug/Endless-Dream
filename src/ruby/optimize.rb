require 'fileutils'

puts "=== Optimizer ==="
project_root = File.expand_path('../..', __dir__)
cleaned_files = 0

Dir.glob(File.join(project_root, '**', '__pycache__')).each do |cache_dir|
    FileUtils.rm_rf(cache_dir)
    puts "-> Removed Python cache: #{cache_dir}"
    cleaned_files += 1
end

Dir.glob(File.join(project_root, '**', '*.pyc')).each do |pyc_file|
    File.delete(pyc_file)
    puts "-> Deleted temporary file: #{pyc_file}"
    cleaned_files += 1
end

puts "-----------------------------------"
puts "Optimization complete! Cleaned items: #{cleaned_files}"
puts "==================================="
require 'fileutils'

source_folder = File.expand_path('../..', __dir__)
backup_folder = File.join(source_folder, 'backups')

FileUtils.mkdir_p(backup_folder)

timestamp = Time.now.strftime('%Y-%m-%d_%H-%M-%S')
destination = File.join(backup_folder, "project_backup_#{timestamp}")

puts "Creating backup at: #{destination}"
FileUtils.mkdir_p(destination)

['src', 'assets'].each do |dir|
    source_dir = File.join(source_folder, dir)
    if Dir.exist?(source_dir)
        FileUtils.cp_r(source_dir, destination)
        puts "-> Folder '#{dir}' copied successfully."
    end
end

backups = Dir.glob(File.join(backup_folder, 'project_backup_*')).sort
if backups.count > 5
    old_backups = backups[0...(backups.count - 5)]
    old_backups.each do |old|
        FileUtils.rm_rf(old)
        puts "-> Cleaned old backup: #{File.basename(old)}"
    end
end

puts "Backup and rotation completed successfully!"
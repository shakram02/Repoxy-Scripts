import matplotlib.pyplot as plt
import file_opener

# TODO: plot all files ?
# TODO: we might want to parse cmd args
log_directory = '/mnt/Exec/code/java/of-Dwoxy/log/'
file_info = file_opener.get_log_files_with_date(log_directory, 'txt')

dates = sorted(file_info.keys())

last_date = dates[-1]
f = open(file_info[last_date])

# Lines are on the following forat: timestamp delay
data = f.readlines()
data = map(lambda s: map(lambda x: x.strip(), s.split(' ')), data)

timestamps = map(lambda s: int(s[0]), data)
delays = map(lambda s: int(s[1]), data)

plt.plot(timestamps, delays)
plt.ylabel('Delay (ns)')
plt.xlabel('Time (ns)')
plt.show()

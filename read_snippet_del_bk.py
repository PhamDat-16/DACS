with open(r'C:\Users\LENOVO\AppData\Roaming\Code\User\History\79dd923\9cEf.html', 'r', encoding='utf-8') as f:
    orig = f.read()

# Let's inspect 9cEf.html between deleteVehicle and bookingForm
pos_del = orig.find('function deleteVehicle')
pos_bk = orig.find('// Bookings System (My Bookings)')
print('pos_del:', pos_del, 'pos_bk:', pos_bk)
snippet = orig[pos_del:pos_bk]
print(snippet.encode('ascii', 'replace').decode('ascii'))

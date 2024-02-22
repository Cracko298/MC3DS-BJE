import json, os, sys

ln0, ln1 = ['fonts','characters'] # Key List names
r0, r1, r2, r3 = ['name','size','pad','type'] # Metadata key names
v0, v1, v2, v3, v4, v5, v6, v7 = ['unicode','x','y','width','height','offset_x','offset_y','advance'] # Keys with values
bsl = b'\x02' # BSL (Byte Seperates Lines) set as var cuz im lazy

def get_rq_name_values(file):
    # Gets the first vars and values for file to work properly.
    with open(file,'rb+') as of:
        data = of.read()
        of.seek(0x38)
        size_val = of.read(1)
        of.seek(0x44)
        padd_val = of.read(1)
        f_offset = data.find(b'mc_10') # Search for key String
        of.seek(f_offset+5)
        if b'_' in of.read(0x01): # Do a little bit of maths if read value is == '_'
            of.seek(f_offset)
            name = of.read(0x08).decode('utf-8')
            bits = 9
        else:
            of.seek(f_offset)
            name = of.read(0x05).decode('utf-8')
            bits = 6

        padd_val = int.from_bytes(padd_val, byteorder='big')
        size_val = int.from_bytes(size_val, byteorder='big')
        of.seek(f_offset + bits) # even more maths
        ff = of.read(0x06).decode('utf-8')

        return { # Return calculated json data
            ln0: [{
                r0: name,
                r1: size_val,
                r2: padd_val,
                r3: ff,
                ln1: []
            }]
        }

file = 'mc_10_ru.bjson' # Currently any font File in .bjson can go here.
print(json.dumps(get_rq_name_values(file), indent=4)) # Debug Information (may remove @ later date)
with open(f'{file.replace('.bjson','_Converted2json.json')}', 'w') as f0:
    json_data = json.dump(get_rq_name_values(file), f0, indent=4)

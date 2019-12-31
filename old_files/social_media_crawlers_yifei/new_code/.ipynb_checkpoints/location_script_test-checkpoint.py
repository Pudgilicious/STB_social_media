import twint

# Obtaining user location
c = twint.Config()
c.Store_object = True
c.Hide_output = True

for user in ["Kasparov63", "ZHENGY14"]:
    c.Username = user
    twint.run.Lookup(c)
    location = twint.output.users_list[-1].location
    print(location)
# %%
import pendulum


# %%
print(pendulum.today())
today = pendulum.today()

# %%
one_year_ago = today.subtract(years=1)

# %%
print(one_year_ago)
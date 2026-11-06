#!/usr/bin/env python
# coding: utf-8

# In[1]:


get_ipython().run_line_magic('pip', 'install matplotlib')


# This chart compares the number of study hours recorded on five weekdays.

# In[2]:


import matplotlib.pyplot as plt

days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
hours = [2, 3, 1, 4, 3]

plt.figure(figsize=(7, 4))
plt.bar(days, hours, color="steelblue")
plt.title("Study Hours During the Week")
plt.xlabel("Day")
plt.ylabel("Study hours")
plt.tight_layout()
plt.show()


# In[3]:


whoami


# In[3]:


print(hidden_value)


# In[4]:


pwd


# In[ ]:





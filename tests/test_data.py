"""
The jwt's here expire 24 hours after issuance. Current expiration is 3/18/2020
16:30 CST
Get a new token at:
https://baseball-agency.auth0.com/authorize?audience=baseball-agency-api&respo
nse_type=token&client_id=pMeaPUNuDQgXjKVckrdVLkYZYVw3cZpx&redirect_uri=https:/
/baseball-agency-api.herokuapp.com
"""

assistant_jwt = '''eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik9ESTRNREZGUXp\
JeVJEQkROVU15TnpRd09VVTFPVEJFTWpVME1VUXhPVEUzT1VRNVJrWkVSZyJ9.eyJpc3MiOiJodHRw\
czovL2Jhc2ViYWxsLWFnZW5jeS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWU2NWJhMmNjNmRiYz\
kwZDNkZTUxYjBhIiwiYXVkIjoiYmFzZWJhbGwtYWdlbmN5LWFwaSIsImlhdCI6MTU4NDQ4MTc0NSwi\
ZXhwIjoxNTg0NTY4MTQ1LCJhenAiOiJwTWVhUFVOdURRZ1hqS1Zja3JkVkxrWVpZVnczY1pweCIsIn\
Njb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZ2V0OmFnZW50cyIsImdldDpwbGF5ZXItZGV0YWlscyIs\
ImdldDp0ZWFtLXJvc3RlciIsImdldDp0ZWFtcyJdfQ.EU8b7ryPGlYZs0_-4_GiWEdbyCe6qhyo903\
wmatQNdPtpZe8sbz0Rcb1-VDARhebJSyh4u7ooSSiI1-lvLMoq1bZvE7y-6Wz1UYs5cwS3W89m-z18\
5KlmtiLw-vdkXrghcSzGvLXUpgiMQzbmpuly78gNBXhCc_cvj6rF5F9WMUt-v0BwPM-m_wQqhz257l\
rGphdAtXXU55q-K-lT8a4ewTzknMXNpg8D13KO2WFEw4_h1LePL9tqj2QBmS5Lyhe7nmaOx-MCWt5p\
YmFBp0IdzIsxGH_ETM7L21QtU3A0P8Ac47okeCvjLyP6ZCLw6ZL9h06OH0DZo8TFexC6asscQ'''

agent_jwt = '''eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik9ESTRNREZGUXpJeVJ\
EQkROVU15TnpRd09VVTFPVEJFTWpVME1VUXhPVEUzT1VRNVJrWkVSZyJ9.eyJpc3MiOiJodHRwczov\
L2Jhc2ViYWxsLWFnZW5jeS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWU2NWJhZWJmN2ZlY2EwZD\
M0OTdiZjU1IiwiYXVkIjoiYmFzZWJhbGwtYWdlbmN5LWFwaSIsImlhdCI6MTU4NDQ4MTcwOSwiZXhw\
IjoxNTg0NTY4MTA5LCJhenAiOiJwTWVhUFVOdURRZ1hqS1Zja3JkVkxrWVpZVnczY1pweCIsInNjb3\
BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOnBsYXllcnMiLCJkZWxldGU6dGVhbXMiLCJnZXQ6\
YWdlbnRzIiwiZ2V0OnBsYXllci1kZXRhaWxzIiwiZ2V0OnRlYW0tZGV0YWlscyIsImdldDp0ZWFtLX\
Jvc3RlciIsImdldDp0ZWFtcyIsInBhdGNoOnBsYXllcnMiLCJwYXRjaDp0ZWFtcyIsInBvc3Q6cGxh\
eWVycyIsInBvc3Q6dGVhbXMiXX0.NHMI7liYZ6y6rHJmQJtB0vrrVhUoL-hic7RpMAAbigLcF8ZVHv\
vwOy4Lle4naN1FjAKqXSnMPsAuN4RcHmn573YFg2TAGhNgDdBHs2Qk3ru1XomBq_Qe6Wz3OJ2LEHta\
oH61Mn0cHe4Dtog8jeRk5h8_19ysW8QA_lteVYb9RJ3Mc8hzQxlUZw-Bp_NQZzGEbYdb0KRwNVrjva\
_uM2lA9lC1lbZ_krKLTjeADlNpPouR7OXpaL6o2LoS6Bh2ug8GiCWWPWbnn_uaSkSNe-FYgtH1IM09\
LhPFsHvyfbar59L8uw7mnnxtw9aS96LJX2nCDul7ubZxzlwvTfaRP2A9BA'''

executive_jwt = '''eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik9ESTRNREZGUXp\
JeVJEQkROVU15TnpRd09VVTFPVEJFTWpVME1VUXhPVEUzT1VRNVJrWkVSZyJ9.eyJpc3MiOiJodHRw\
czovL2Jhc2ViYWxsLWFnZW5jeS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWU2NWJiNTBmN2ZlY2\
EwZDM0OTdjMDM4IiwiYXVkIjoiYmFzZWJhbGwtYWdlbmN5LWFwaSIsImlhdCI6MTU4NDQ4MTY2Nywi\
ZXhwIjoxNTg0NTY4MDY3LCJhenAiOiJwTWVhUFVOdURRZ1hqS1Zja3JkVkxrWVpZVnczY1pweCIsIn\
Njb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFnZW50cyIsImdldDphZ2VudC1jbGllbnRz\
IiwiZ2V0OmFnZW50LWRldGFpbHMiLCJnZXQ6YWdlbnRzIiwiZ2V0OnBsYXllci1kZXRhaWxzIiwiZ2\
V0OnRlYW0tZGV0YWlscyIsImdldDp0ZWFtLXJvc3RlciIsImdldDp0ZWFtcyIsInBhdGNoOmFnZW50\
cyIsInBvc3Q6YWdlbnRzIl19.tA7YY7RHVnyUUzOo9U_Bn573yqM-6ELe4r-nCHcYoSPtDKKIGHFCg\
EB-zEIZ-LsaiDCoGdE618jcpFnp1I6K_zo6atzmTnhqzKS-vU3ULHKY0VBzHa0-ne-bCmnBRQHrkQk\
9VBjzZmwVTlcgv5TFPNnVkpXiHrGzeQuIIS6Kylkjru0n4fWMgS6HEOl7d61ZWm8Xeq9ddiHdmwlJR\
xqArEQOnVuf2SRAK2uQ5yE7fonLl1p0h2Ellop-V56nXv_u4rVuO69GNxvA4Cfelu5dAovOhNRE5E_\
aOZ3DliXVzWkEMd5EXOYYLqyT5paRcp5yIME_r6_TABD6Typa1efYKw'''
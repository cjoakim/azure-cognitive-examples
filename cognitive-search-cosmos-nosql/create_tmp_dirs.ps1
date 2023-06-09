# Create the necessary tmp/ directories as they are git-ignored.
#
# Chris Joakim, Microsoft

new-item -itemtype directory -force -path .\py_acs_admin\tmp     | Out-Null
new-item -itemtype directory -force -path .\java_acs_client\app\tmp  | Out-Null
new-item -itemtype directory -force -path .\java_acs_client\tmp  | Out-Null
new-item -itemtype directory -force -path .\py_cosmos_data\tmp   | Out-Null

Write-Output 'done'
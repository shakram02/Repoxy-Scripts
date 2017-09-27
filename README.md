# Dimensional Gate Scripts 
 
Scripts that make life easier in automation and benchmarking 
- Plots 
- Test automation 
- Forwarding controller component 
 
## Test automation 
A messenger sends commands from the mininet VM to the other VMs so that they
execute and tear down the controller processes 
The test bed contains at least 2 VMs both of which are mininet VMs. The first
VM's purpose is to run mininet only, the other VMs run the controller  
only. The test and automation scripts will handle that for you. So mainly, all 
what you need is to run the test scripts. 
 
To run the tests the simple wat 
1) launch `sync-to-vm.sh` in both the mininet VM and the other VM 
2) launch `test_automation/messenger/command_receiver/message_receiver.py` in
the controller VM 
3) launch `test_automation/test_one_controller.py` in the network VM 


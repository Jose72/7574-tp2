xterm -title "App 1" -hold -e "python3 ./main_ventilator.py" &
xterm -title "App 6" -hold -e "python3 ./main_sink.py" &
xterm -title "App 2" -hold -e "python3 ./test/basic_client_send.py" &
xterm -title "App 3" -hold -e "python3 ./main_worker.py" &
xterm -title "App 4" -hold -e "python3 ./main_worker.py" &
xterm -title "App 5" -hold -e "python3 ./main_worker.py"



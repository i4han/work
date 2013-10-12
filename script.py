import applescript

script = applescript.AppleScript("""
    on readcell(x, y)
	    tell application "Numbers"
	    	tell document "Untitled" 
	    		tell sheet "Sheet 3"
	    			tell table "Table 1"
	    				set a to value of cell y of column x
	    			end tell
	    		end tell
	    	end tell
	    end tell

    end
""")

print script.call('readcell', 1, 1)


"""
	    tell application "Numbers" to tell document "Untitled" tell sheet "Sheet 3" to tell table "Table 1"
	    	set a to value of cell y of column x
	    end tell
"""
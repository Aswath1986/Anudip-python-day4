"""
Practice 4: else and finally
else    -> runs only when there was NO error
finally -> runs ALWAYS
"""

def check_age(text):
    print("Checking:", text)
    try:
        age = int(text)
    except ValueError:
        print("  except : that is not a number")
    else:
        print("  else   : age is", age)
    finally:
        print("  finally: check complete")


check_age("21")
check_age("twenty")

# Try it yourself:
#   Predict the output for check_age("0") and then run it

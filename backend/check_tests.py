import traceback
try:
    import tests.test_session
    print("Import OK")
except Exception as e:
    with open("tb.txt", "w", encoding="utf-8") as f:
        f.write(traceback.format_exc())

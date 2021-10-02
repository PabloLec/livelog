from subprocess import Popen, PIPE


def test_default(default_log_file):
    process = Popen("timeout 2 python3 -m livelog".split(), stdout=PIPE)
    out, err = process.communicate()
    assert "It works" in str(out)

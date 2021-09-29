from logger import Logger

logger = Logger()
print(logger.output_file)  # = "/tmp/test"
while True:
    logger.error("C'est une erreur")
    logger.warn("Juste un warning")
    logger.info("Une info")
    logger.debug("Du debugging")
    import time

    time.sleep(0.1)

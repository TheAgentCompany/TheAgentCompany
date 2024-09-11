FROM base-image

# persist evaluator and task files in the exam image
COPY evaluator.py /evaluation/
COPY task.md /instruction/

# requests library is needed for evaluation (optional)
RUN pip install requests

# copy and run initialization code (optional)
COPY init.sh /
COPY init.py /

# Set NPC ENV
COPY scenarios.json /npc
ENV OPENAI_API_KEY sk-AkN51Iu09G5lKoGZK2_As-lO8dqKyyWWysP4bdljoMT3BlbkFJa92oLQHtXfhP3ylgAVPLJ9jkB7BJTGVV1aFvofHTcA
ENV REDIS_OM_URL redis://default:jobbench@ogma.lti.cs.cmu.edu/:6379
ENV BOT_URL http://ogma.lti.cs.cmu.edu:3000

# Run init
RUN chmod +x /init.sh
RUN sh /init.sh
RUN python /init.py

# Set up NPC environment and keep the container running (optional)
CMD python /npc/run_multi_npc.py && tail -f /dev/null

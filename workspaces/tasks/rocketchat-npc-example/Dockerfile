FROM base-npc-image

# Step1: Set ENV: OPENAI API KEY, REDIS_OM_URL, BOT_URL
ENV OPENAI_API_KEY <Your OPENAI_API_KEY>
# Redis Username: default, Password: jobbench
# Redis service URL: ogma.lti.cs.cmu.edu/:6379
ENV REDIS_OM_URL redis://default:jobbench@ogma.lti.cs.cmu.edu/:6379
# RocketChat service URL
ENV BOT_URL http://ogma.lti.cs.cmu.edu:3000

# Step2: Change the scenarios.json to use your own definition
COPY scenarios.json /npc
# Step3: Execute the run_multi_npc.py in npc directory. Pay attention you need to execute it under /npc, we already configure the file path env in base-npc-image
#        If you also have other command to execute, put python run_multi_npc.py and others into scripts. Dockerfile only allow one CMD
#        run_multi_npc.py will launch the npc in backgroud then exit. In example, we sleep to keep docker running. You don't need to do it in examinee
CMD python /npc/run_multi_npc.py && sleep 1000000
# CMD ["tail", "-f","/dev/null"]
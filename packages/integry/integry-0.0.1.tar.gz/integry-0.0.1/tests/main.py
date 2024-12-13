from integry import Integry

user_id = "moiz@integry.io"


async def main():
    async with Integry(
        app_secret="9c3bc159-0600-40c8-8b89-05f3f648e7b5",
        app_key="f6ece551-720c-4514-bba2-10f5847c44de",
    ) as integry:
        # print(await integry.apps.get("agendor", user_id))
        # return
        # data = await integry.functions.call("slack-post-message", {"channel": "test_slack", "text": "?"}, user_id)
        # predictions = await integry.functions.predict(prompt="fetch all my conversations on Slack", user_id=user_id, predict_arguments=True)
        # predictions = await integry.functions.predict(prompt="say hello to my team on Slack", user_id=user_id, predict_arguments=True)
        # if predictions:
        #     function = predictions[0]
        #     r = await function(user_id, function.arguments)
        #     print(r)
        # page = await integry.functions.list(user_id, include=["meta"])

        # page = await integry.functions.list("moiz@integry.io", cursor=page.cursor)

        async for function in integry.functions.list(user_id):
            print(function)
            # await function(user_id, {})
            break

        # page = await integry.functions.call("moiz@integry.io", "test")
        # for function in page.functions:
        # await function({"id": 1})
        # print(page)

        
        
        # async for app in integry.apps.list(user_id):
            # print(app.name)

        cursor = ""
        while False:
            page = await integry.apps.list(user_id, cursor=cursor)
            # print(page.cur)
            for app in page.apps:
                print(f"--: {app.name}")
            if not page.cursor:
                break
            cursor = page.cursor

        # async for app in integry.apps.list(user_id):
        # print(f"--: {app.name}")
        # print(page)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())

# PYTHONPATH=src python tests/main.py python tests/main.py

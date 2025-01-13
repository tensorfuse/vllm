## To deploy using Tensorfuse use this

```
tensorkube deploy --gpus 4 --gpu-type L40S --secret hugging-face-secret
```


## To query the endpoint

You can get the endpoint using `tensorkube deployment list`

```
curl --request POST -v \
  --url <endpoint>/v1/chat/completions \
  --header 'Content-Type: application/json' \
  --data '{
  "model": "gane5hvarma/joe-adapter",
  "messages": [
    {
      "role": "user",
      "content": "hello"
    }
  ]
}'
```

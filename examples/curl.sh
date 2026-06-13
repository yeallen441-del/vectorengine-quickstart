curl https://www.vectronode.com/v1/chat/completions \
  -H "Authorization: Bearer $VECTORNODE_API_KEY" \
  -H "Content-Type: application/json" \
  -d "{
    \"model\": \"$VECTORNODE_MODEL\",
    \"messages\": [
      {
        \"role\": \"user\",
        \"content\": \"Hello from VectorNode\"
      }
    ]
  }"

HALT_CHAT_STREAM_MUTATION: str = """
  mutation HaltChatStream($chatUuid: UUID!) {
    haltChatStream(chatUuid: $chatUuid) {
      __typename
    }
  }
"""


MOVE_CHAT_TO_CLOUD_MUTATION: str = """
  mutation MoveChatToCloud($chatUuid: UUID!) {
    moveChatToCloud(chatUuid: $chatUuid) {
      ... on Chat {
        chatUuid
        name
      }
      ... on UnauthenticatedError {
        message
      }
      ... on ChatNotFoundError {
        message
      }
      ... on CloudSessionError {
        message
        chatUuid
      }
    }
  }
"""


SET_LOGIN_COMPLETE_MUTATION: str = """
  mutation SetLoginComplete {
    setLoginComplete {
      __typename
      ... on User {
        userApiKey
      }
      ... on UnauthenticatedError {
        message
      }
    }
  }
"""


UPGRADE_USER_TO_TRUSTED_MUTATION: str = """
  mutation UpgradeUserToTrusted($email: String!) {
    upgradeUserToTrusted(email: $email) {
      __typename
      ... on User {
        email
        plan
      }
      ... on Error {
        message
      }
    }
  }
"""


REFRESH_API_KEY_MUTATION = """
mutation RefreshApiKey {
    refreshApiKey {
        ... on User {
            userApiKey
        }
        ... on UnauthenticatedError {
            message
        }
    }
}
"""

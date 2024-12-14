use crate::{
    config::Config,
    error::TupleleapAIError,
    types::{CreateModerationRequest, CreateModerationResponse},
    Client,
};

/// Given text and/or image inputs, classifies if those inputs are potentially harmful across several categories.
///
/// Related guide: [Moderations](https://platform.TupleleapAI.com/docs/guides/moderation)
pub struct Moderations<'c, C: Config> {
    client: &'c Client<C>,
}

impl<'c, C: Config> Moderations<'c, C> {
    pub fn new(client: &'c Client<C>) -> Self {
        Self { client }
    }

    /// Classifies if text and/or image inputs are potentially harmful. Learn
    /// more in the [moderation guide](https://platform.TupleleapAI.com/docs/guides/moderation).
    pub async fn create(
        &self,
        request: CreateModerationRequest,
    ) -> Result<CreateModerationResponse, TupleleapAIError> {
        self.client.post("/moderations", request).await
    }
}

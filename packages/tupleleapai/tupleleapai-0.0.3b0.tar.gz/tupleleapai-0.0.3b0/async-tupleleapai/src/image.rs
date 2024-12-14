use crate::{
    config::Config,
    error::TupleleapAIError,
    types::{
        CreateImageEditRequest, CreateImageRequest, CreateImageVariationRequest, ImagesResponse,
    },
    Client,
};

/// Given a prompt and/or an input image, the model will generate a new image.
///
/// Related guide: [Image generation](https://platform.TupleleapAI.com/docs/guides/images)
pub struct Images<'c, C: Config> {
    client: &'c Client<C>,
}

impl<'c, C: Config> Images<'c, C> {
    pub fn new(client: &'c Client<C>) -> Self {
        Self { client }
    }

    /// Creates an image given a prompt.
    pub async fn create(&self, request: CreateImageRequest) -> Result<ImagesResponse, TupleleapAIError> {
        self.client.post("/images/generations", request).await
    }

    /// Creates an edited or extended image given an original image and a prompt.
    pub async fn create_edit(
        &self,
        request: CreateImageEditRequest,
    ) -> Result<ImagesResponse, TupleleapAIError> {
        self.client.post_form("/images/edits", request).await
    }

    /// Creates a variation of a given image.
    pub async fn create_variation(
        &self,
        request: CreateImageVariationRequest,
    ) -> Result<ImagesResponse, TupleleapAIError> {
        self.client.post_form("/images/variations", request).await
    }
}

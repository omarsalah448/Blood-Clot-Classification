namespace Mayo_Clinic.Repository
{
    public interface IAPIRepository
    {
        Task<HttpResponseMessage> Request(string resource, dynamic requestBody);
    }
}


using Microsoft.Extensions.Configuration;
using System.Configuration;
using System.Text;
using System.Text.Json;

namespace Mayo_Clinic.Repository
{
    public class APIRepository : IAPIRepository
    {
        private readonly IConfiguration configuration;
        public APIRepository(IConfiguration _configuration) {
            configuration = _configuration;
        }
        public async Task<HttpResponseMessage> Request(string resource, dynamic requestBody)
        {
            using (HttpClient httpClient = new HttpClient())
            {
                // build the URL
                string server = configuration.GetValue<string>("API:LocalServer");
                string port = configuration.GetValue<string>("API:Port");
                string url = $"http://{server}:{port}/{resource}";
                Console.WriteLine(requestBody);
                var jsonContent = JsonSerializer.Serialize(requestBody);
                var httpContent = new StringContent(jsonContent, Encoding.UTF8, "application/json");
                HttpResponseMessage response = await httpClient.PostAsync(url, httpContent);
                return response;
            }
        }
    }
}

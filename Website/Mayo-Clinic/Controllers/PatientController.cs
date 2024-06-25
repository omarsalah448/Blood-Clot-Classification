using Mayo_Clinic.Models;
using Mayo_Clinic.Repository;
using Mayo_Clinic.ViewModels;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Identity;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Options;
using Microsoft.Identity.Client;
using Newtonsoft.Json.Linq;
using System.Net.Http;
using System.Security.Policy;
using System.Text;
using System.Text.Json;


namespace Mayo_Clinic.Controllers
{
    [Authorize]
    public class PatientController : Controller
    {
        private readonly IDoctorRepository doctorRepository;
        private readonly IPatientRepository patientRepository;
        private readonly IAPIRepository apiRepository;
        private readonly UserManager<ApplicationUser> userManager;
        private readonly IConfiguration configuration;

        public PatientController(IDoctorRepository _doctorRepository, IPatientRepository _patientRepository,
               IAPIRepository _apiRepository, UserManager<ApplicationUser> _userManager, IConfiguration _configuration)
        {
            doctorRepository = _doctorRepository;
            patientRepository = _patientRepository;
            apiRepository = _apiRepository;
            userManager = _userManager;
            configuration = _configuration;
        }

        [HttpGet]
        public IActionResult Add()
        {
            return View();
        }
        [HttpPost]
        [ValidateAntiForgeryToken]
        public IActionResult Add(Patient patient)
        {
            patient.Docotor_Id = doctorRepository.GetSignedInDoctorID();
            if (ModelState.IsValid)
            {
                patientRepository.Insert(patient);
                return RedirectToAction("ViewAll");
            }
            return View(patient);
        }
        [HttpGet]
        public IActionResult Edit(int Id)
        {
            Console.WriteLine("ops wrong function");
            Patient patient = patientRepository.GetById(Id);
            return View(patient);
        }
        [HttpPost]
        [ValidateAntiForgeryToken]
        public IActionResult Edit(Patient patient)
        {
            Console.WriteLine("here in the first place");
            if (ModelState.IsValid)
            {
                patientRepository.Edit(patient);
                return RedirectToAction("ViewAll");
            }
            Console.WriteLine(ModelState.ToString());
            return View(patient);
        }
        [HttpPost]
        [ValidateAntiForgeryToken]
        public IActionResult Delete(int Id)
        {
            patientRepository.Delete(Id);
            return RedirectToAction("ViewAll");
        }
        [HttpGet]
        public IActionResult ViewAll()
        {
            string Id = doctorRepository.GetSignedInDoctorID();
            List<Patient> patients = doctorRepository.GetPatientsByDrID(Id);
            List<DisplayPatientViewModel> patientsVM = new List<DisplayPatientViewModel>();
            foreach (Patient patient in patients)
            {
                patientsVM.Add(new DisplayPatientViewModel
                {
                    Id = patient.Id,
                    Name = patient.Name,
                    PhoneNumber = patient.PhoneNumber,
                    Age = doctorRepository.GetAgeByBirthDate(patient.BirthDate),
                    Classification = patient.Classification
                });
            }
            return View(patientsVM);
        }
        public IActionResult Details(int id)
        {
            Patient patient = patientRepository.GetById(id);
            ProfilePatientViewModel patientVM = new ProfilePatientViewModel
            {
                Id = patient.Id,
                Name = patient.Name,
                PhoneNumber = patient.PhoneNumber,
                Age = doctorRepository.GetAgeByBirthDate(patient.BirthDate),
                BloodClotImage = patient.BloodClotImage,
                Classification = patient.Classification
            };
            return View(patientVM);
        }

        [HttpGet]
        public async Task<IActionResult> Predict(int id)
        {
            Patient patient = patientRepository.GetById(id);
            try
            {
                var requestBody = new
                {
                    image_path = patient.BloodClotImage
                };

                HttpResponseMessage response = await apiRepository.Request("predict", requestBody);
                if (response.IsSuccessStatusCode)
                {
                    string responseContent = await response.Content.ReadAsStringAsync();
                    JObject jsonResponse = JObject.Parse(responseContent);
                    string prediction = jsonResponse["prediction"].ToString();
                    patient.Classification = prediction;
                    patientRepository.Edit(patient);
                    return RedirectToAction("ViewAll");
                }
                else
                {
                    return Content("Error: " + response.StatusCode);
                }
            }
            catch (Exception ex)
            {
                return Content("Error: " + ex.Message);
            }
        }
        [HttpGet]
        public async Task<IActionResult> Explain(int id)
        {
            Patient patient = patientRepository.GetById(id);
            try
            {
                var requestBody = new
                {
                    image_path = patient.BloodClotImage
                };

                HttpResponseMessage response = await apiRepository.Request("explain", requestBody);
                if (response.IsSuccessStatusCode)
                {
                    string responseContent = await response.Content.ReadAsStringAsync();
                    JObject jsonResponse = JObject.Parse(responseContent);
                    string image = jsonResponse["image"].ToString();
                    return Content(image);
                }
                else
                {
                    return Content("Error: " + response.StatusCode);
                }
            }
            catch (Exception ex)
            {
                return Content("Error: " + ex.Message);
            }
        }

    }






    //    public async Task<IActionResult> Predict()
    //    {
    //        try
    //        {
    //            using (HttpClient httpClient = new HttpClient())
    //            {
    //                Console.WriteLine("first");
    //                // build the URL
    //                string server = configuration.GetValue<string>("API:LocalServer");
    //                string port = configuration.GetValue<string>("API:Port");
    //                string predictUrl = $"http://{server}:{port}/predict";
    //                Console.WriteLine("predicturl", predictUrl);
    //                var requestBody = new
    //                {
    //                    image_path = "008e5c_0.tif"
    //                };
    //                var jsonContent = JsonSerializer.Serialize(requestBody);
    //                var httpContent = new StringContent(jsonContent, Encoding.UTF8, "application/json");
    //                HttpResponseMessage response = await httpClient.PostAsync(predictUrl, httpContent);
    //                Console.WriteLine("before if");
    //                    if (response.IsSuccessStatusCode)
    //                    {
    //                        Console.WriteLine("if success");
    //                        string responseContent = await response.Content.ReadAsStringAsync();
    //    JObject jsonResponse = JObject.Parse(responseContent);
    //    string prediction = jsonResponse["prediction"].ToString();

    //                        return Content(responseContent);
    //}
    //                    else
    //{
    //    Console.WriteLine("if fail");
    //    return Content("Error: " + response.StatusCode);
    //}
    //            }
    //        }
    //        catch (Exception ex)
    //        {
    //            return Content("Error: " + ex.Message);
    //        }
    //    }

    //}
}

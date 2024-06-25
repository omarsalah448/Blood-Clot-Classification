using Mayo_Clinic.Models;
using Mayo_Clinic.Repository;
using Mayo_Clinic.ViewModels;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Identity;
using Microsoft.AspNetCore.Mvc;
using System.Security.Claims;

namespace Mayo_Clinic.Controllers
{
    [Authorize]
    public class DoctorController : Controller
    {
        private readonly IDoctorRepository doctorRepository;
        private readonly IPatientRepository patientRepository;
        private readonly UserManager<ApplicationUser> userManager;
        public DoctorController(IDoctorRepository _doctorRepository, IPatientRepository _patientRepository,
               UserManager<ApplicationUser> _userManager)
        {
            doctorRepository = _doctorRepository;
            patientRepository = _patientRepository;
            userManager = _userManager;
        }
        public IActionResult Index()
        {
            return RedirectToAction("Profile");
        }
        [HttpGet]
        public async Task<IActionResult> EditProfile()
        {
            string id = doctorRepository.GetSignedInDoctorID();
            Doctor doctor = doctorRepository.GetById(id);
            ApplicationUser user = await userManager.FindByIdAsync(id);
            RegisterDoctorViewModel viewModel = new RegisterDoctorViewModel
            {
                FirstName = user.FirstName,
                LastName = user.LastName,
                PhoneNumber = user.PhoneNumber,
                Email = user.Email,
                UserName = user.UserName,
                University = doctor.University,
                Description = doctor.Description,
                Image = doctor.Image,
            };
            return View(viewModel);
        }
        [HttpPost]
        public async Task<IActionResult> EditProfile(RegisterDoctorViewModel doctor)
        {
            if (ModelState.IsValid)
            {
                string id = doctorRepository.GetSignedInDoctorID();
                await doctorRepository.Edit(id, doctor);
                return RedirectToAction("Profile");
            }
            else
            {
                var errors = ModelState.Values.SelectMany(v => v.Errors.Select(e => e.ErrorMessage));

                foreach (var error in errors)
                {
                    ModelState.AddModelError("", error);
                }
                return View(doctor);
            }
        }

        [HttpGet]
        public async Task<IActionResult> Profile()
        {
            string Id = doctorRepository.GetSignedInDoctorID();
            Doctor doctor = doctorRepository.GetById(Id);
            ApplicationUser user = await userManager.FindByIdAsync(Id);
            ProfileDoctorViewModel doctorVM = new ProfileDoctorViewModel {
                    FirstName = user.FirstName,
                    LastName = user.LastName,
                    UserName = user.UserName,
                    University = doctor.University,
                    Description = doctor.Description,
                    Image = doctor.Image
                };
            return View(doctorVM);
        }
    }
}

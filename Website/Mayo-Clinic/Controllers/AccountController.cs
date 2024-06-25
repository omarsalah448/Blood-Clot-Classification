using Mayo_Clinic.Models;
using Mayo_Clinic.Repository;
using Mayo_Clinic.ViewModels;
using Microsoft.AspNetCore.Identity;
using Microsoft.AspNetCore.Mvc;

namespace Mayo_Clinic.Controllers
{
    public class AccountController : Controller
    {
        private readonly UserManager<ApplicationUser> userManager;
        private readonly SignInManager<ApplicationUser> signInManager;
        private readonly IDoctorRepository doctorRepository;
        public AccountController(UserManager<ApplicationUser> _userManager, 
               SignInManager<ApplicationUser> _signInManager, 
               IDoctorRepository _doctorRepository)
        {
            userManager = _userManager;
            signInManager = _signInManager;
            doctorRepository = _doctorRepository;
        }
        public IActionResult Index()
        {
            return View();
        }
        [HttpGet]
        public IActionResult Register() { 
            return View();
        }
        [HttpPost]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> Register(RegisterDoctorViewModel doctorVM)
        {
            if (ModelState.IsValid)
            {
                ApplicationUser appUser = new ApplicationUser();
                appUser.FirstName = doctorVM.FirstName;
                appUser.LastName = doctorVM.LastName;
                appUser.Email = doctorVM.Email;
                appUser.UserName = doctorVM.UserName;
                appUser.PasswordHash = doctorVM.Password;

                IdentityResult result = await userManager.CreateAsync(appUser, doctorVM.Password);
                if (result.Succeeded)
                {
                    // create a doctor with the same id for the user
                    Doctor doctor = new Doctor
                    {
                        // use the same Id as ApplicationUser
                        Id = appUser.Id, 
                        University = doctorVM.University,
                        Description = doctorVM.Description,
                        Image = doctorVM.Image
                    };
                    doctorRepository.Insert(doctor);
                    await signInManager.SignInAsync(appUser, isPersistent: false);
                    return RedirectToAction("Profile", "Doctor");
                } else
                {
                    foreach (var err in result.Errors)            
                        ModelState.AddModelError("", err.Description);
                }
            }
            return View(doctorVM);
        }
        [HttpGet]
        public async Task<IActionResult> SignIn()
        {
            return View();
        }
        [HttpPost]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> SignIn(SignInViewModel signInVM)
        {
            if (ModelState.IsValid)
            { 
                ApplicationUser appUser = await userManager.FindByNameAsync(signInVM.UserName);
                if (appUser != null)
                {
                    bool ok = await userManager.CheckPasswordAsync(appUser, signInVM.Password);
                    if (ok) {
                        await signInManager.SignInAsync(appUser, signInVM.RememberMe);
                        return RedirectToAction("Profile", "Doctor");
                    }
                }
                else
                {
                    ModelState.AddModelError("", "Invalid User Name and Password");
                }
            }
            return View(signInVM);
        }
        [HttpGet]
        public async Task<IActionResult> SignOut()
        {
            await signInManager.SignOutAsync();
            return RedirectToAction("SignIn");
        }
    }
}

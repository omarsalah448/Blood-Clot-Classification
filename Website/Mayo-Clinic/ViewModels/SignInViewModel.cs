using System.ComponentModel.DataAnnotations;

namespace Mayo_Clinic.ViewModels
{
    public class SignInViewModel
    {
        [Required]
        [Display(Name = "User Name:")]
        public string UserName { get; set; } = string.Empty;

        [Required]
        [Display(Name = "Password:")]
        [DataType(DataType.Password)]
        public string Password { get; set; } = string.Empty;

        [Display(Name = "Remember Me:")]
        public bool RememberMe { get; set; }
    }
}
